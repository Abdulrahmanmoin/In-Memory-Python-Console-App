# Data Model: Full-Stack Web Application

## Entity Definitions

### User Entity
- **user_id**: UUID (Primary Key) - Unique identifier for each user
- **email**: String - User's email address (unique, required)
- **username**: String - User's chosen username (unique, required)
- **hashed_password**: String - Bcrypt hashed password (required)
- **created_at**: DateTime - Timestamp when user account was created
- **updated_at**: DateTime - Timestamp when user account was last updated
- **is_active**: Boolean - Whether the user account is active (default: true)

### Task Entity
- **task_id**: UUID (Primary Key) - Unique identifier for each task
- **user_id**: UUID (Foreign Key) - Reference to the owning user
- **title**: String - Task title or description (required, max 200 chars)
- **description**: Text - Detailed task description (optional)
- **is_completed**: Boolean - Whether the task is completed (default: false)
- **created_at**: DateTime - Timestamp when task was created
- **updated_at**: DateTime - Timestamp when task was last updated
- **completed_at**: DateTime - Timestamp when task was marked as completed (nullable)

## Entity Relationships

### User → Task (One-to-Many)
- One user can own multiple tasks
- Foreign key constraint: task.user_id references user.user_id
- Cascade delete: When a user is deleted, all their tasks are also deleted
- Required relationship: Every task must belong to a user

## Validation Rules

### User Validation
- Email must follow standard email format
- Email and username must be unique across all users
- Password must meet minimum security requirements (will be validated during registration)
- Username must not be empty and contain only allowed characters

### Task Validation
- Title must not be empty and have maximum length of 200 characters
- Task must belong to a valid user (foreign key constraint)
- User can only access/modify tasks they own
- Description can be empty but has maximum length of 1000 characters

## Database Constraints

### Primary Keys
- Both User and Task entities use UUID primary keys for global uniqueness
- Primary keys are auto-generated on entity creation

### Foreign Keys
- Task.user_id references User.user_id with CASCADE delete
- Database enforces referential integrity

### Unique Constraints
- User.email: Unique constraint to prevent duplicate email addresses
- User.username: Unique constraint to prevent duplicate usernames

### Indexes
- Index on User.email for efficient authentication lookups
- Index on Task.user_id for efficient user-specific queries
- Index on Task.is_completed for filtering completed tasks
- Composite index on (Task.user_id, Task.created_at) for efficient user task retrieval

## State Transitions

### Task State Transitions
- **Pending → Completed**: When user marks task as complete
  - Set is_completed = true
  - Set completed_at = current timestamp
- **Completed → Pending**: When user unmarks task as complete
  - Set is_completed = false
  - Set completed_at = null

### User State Transitions
- **Active → Inactive**: When account is deactivated
  - Set is_active = false
  - Prevents authentication and access to resources

## API Contract Implications

### User Data Exposure
- User entity data exposed through API endpoints will exclude sensitive fields (hashed_password)
- Only user's own data will be accessible through API calls

### Task Data Exposure
- Task entities will be returned with user_id for reference but users can only access their own tasks
- API will enforce user ownership validation on all task operations