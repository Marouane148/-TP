# TP Analysis: Distance Calculator Application

## Initial Assessment

### Current Test Coverage
**Coverage before modifications: 0%**
- No test files exist in the repository
- No test configuration files (.pytest.ini, setup.cfg, pyproject.toml)
- All code is untested

### Code Quality Issues Identified

#### 1. Code Style & Naming
- **Issue**: Inconsistent variable naming (eNd, startPoint, StartPoint, EndPoint)
- **Impact**: Reduces readability and maintainability
- **Severity**: High

#### 2. Code Duplication
- **Issue**: Distance calculation formula appears in 2 places
- **Impact**: Violates DRY principle, increases bug surface area
- **Severity**: High

#### 3. API Design Issues
- **Issue**: `/api/distance` accepts GET, POST, and PUT but processes all the same way
- **Issue**: No proper HTTP status codes returned
- **Impact**: Non-RESTful API, unpredictable behavior
- **Severity**: Critical

#### 4. Input Validation
- **Issue**: No validation of coordinate format, data types, or boundary conditions
- **Impact**: Application crashes on invalid input
- **Severity**: Critical

#### 5. Error Handling
- **Issue**: No try/catch blocks anywhere
- **Severity**: Critical

#### 6. State Management
- **Issue**: Global `distances = list()` without persistence or size limits
- **Severity**: Medium

#### 7. Comments
- **Issue**: Minimal, inline French comments that restate code
- **Assessment**: Not particularly helpful
- **Recommendation**: Remove and use better code structure instead

#### 8. HTML Template
- **Issue**: No form labels, validation hints, or proper structure
- **Severity**: Medium

## REST API Compliance Analysis

**Does the API follow REST principles? NO**

### Evidence:
- GET method should be idempotent (currently has side effects)
- No proper HTTP status codes
- No error responses
- Mixed HTTP methods with same logic
- Stateful GET operations

## Testing Framework Assessment

**Framework Used**: None initially → pytest v8.4.2 after

**Configuration**: pytest.ini with test discovery and markers

## Technical Debt Summary

| Category | Items | Priority |
|---|---|---|
| **Code Quality** | Duplication, naming, structure | High |
| **Testing** | 0% coverage, no test infrastructure | Critical |
| **API Design** | Non-RESTful, no validation | Critical |
| **Error Handling** | No try/catch, no error responses | Critical |
| **Documentation** | No docstrings, minimal comments | Medium |
| **Security** | No input validation | High |
| **Performance** | Unbounded list, no indexing | Medium |

