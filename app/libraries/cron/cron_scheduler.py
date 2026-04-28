"""
Cron Expression Parser and Task Scheduler.

Supports standard cron format: minute hour day month dow (day of week)
Special characters: * (any), ? (no specific value), - (range), , (list), / (step)
"""
from datetime import datetime, timedelta
from typing import Any, Callable, Dict, List, Optional
from enum import IntEnum


class CronField(IntEnum):
    """Field indices for cron expression."""
    MINUTE = 0
    HOUR = 1
    DAY_OF_MONTH = 2
    MONTH = 3
    DAY_OF_WEEK = 4


class CronExpression:
    """Parses and evaluates cron expressions."""

    MINUTE_RANGE = range(0, 60)
    HOUR_RANGE = range(0, 24)
    DAY_RANGE = range(1, 32)
    MONTH_RANGE = range(1, 13)
    DAY_OF_WEEK_RANGE = range(0, 7)  # 0=Sunday, 6=Saturday

    MONTH_NAMES = {
        'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 'may': 5, 'jun': 6,
        'jul': 7, 'aug': 8, 'sep': 9, 'oct': 10, 'nov': 11, 'dec': 12
    }

    DAY_NAMES = {
        'sun': 0, 'mon': 1, 'tue': 2, 'wed': 3, 'thu': 4, 'fri': 5, 'sat': 6
    }

    def __init__(self, expression: str):
        """
        Initialize with a cron expression string.

        Args:
            expression: Standard cron format "minute hour day month dow"
        """
        self.expression = expression.strip()
        self.fields = self._parse_expression()

    def _parse_expression(self) -> List[set]:
        """
        Parse cron expression into a list of sets for each field.

        Returns:
            List of 5 sets representing valid values for each field
        """
        parts = self.expression.split()
        if len(parts) != 5:
            raise ValueError(f"Invalid cron expression: expected 5 fields, got {len(parts)}")

        field_ranges = [
            self.MINUTE_RANGE,
            self.HOUR_RANGE,
            self.DAY_RANGE,
            self.MONTH_RANGE,
            self.DAY_OF_WEEK_RANGE
        ]

        fields = []
        for i, part in enumerate(parts):
            fields.append(self._parse_field(part, field_ranges[i], i))

        return fields

    def _parse_field(self, field_str: str, value_range, field_index: int) -> set:
        """
        Parse a single cron field.

        Args:
            field_str: The field string (e.g., "*/15", "1-5", "1,3,5")
            value_range: The valid range for this field
            field_index: Index of the field (for month/day name lookup)

        Returns:
            Set of valid values for this field
        """
        field_str = field_str.lower().strip()

        # Handle wildcard
        if field_str == '*':
            return set(value_range)

        # Handle question mark (used for day or day of week to mean "no specific value")
        if field_str == '?':
            return set(value_range)

        # Handle step values (*/5, 10-50/5, etc.)
        if '/' in field_str:
            return self._parse_step(field_str, value_range, field_index)

        # Handle ranges (1-5)
        if '-' in field_str:
            return self._parse_range(field_str, value_range, field_index)

        # Handle lists (1,3,5)
        if ',' in field_str:
            values = set()
            for part in field_str.split(','):
                part = part.strip()
                if part in self._get_names_for_field(field_index):
                    values.add(self._get_names_for_field(field_index)[part])
                else:
                    try:
                        values.add(int(part))
                    except ValueError:
                        raise ValueError(f"Invalid cron value: {part}")
            return values & set(value_range)

        # Handle single value or name
        if field_str in self._get_names_for_field(field_index):
            return {self._get_names_for_field(field_index)[field_str]} & set(value_range)

        try:
            value = int(field_str)
            if value not in value_range:
                raise ValueError(f"Value {value} out of range {value_range}")
            return {value}
        except ValueError as e:
            raise ValueError(f"Invalid cron value: {field_str}") from e

    def _parse_range(self, range_str: str, value_range, field_index: int) -> set:
        """Parse range expressions like 1-5."""
        parts = range_str.split('-')
        if len(parts) != 2:
            raise ValueError(f"Invalid range: {range_str}")

        start_str, end_str = parts[0].strip(), parts[1].strip()
        names = self._get_names_for_field(field_index)

        start = names.get(start_str, None)
        if start is None:
            try:
                start = int(start_str)
            except ValueError:
                raise ValueError(f"Invalid range start: {start_str}")

        end = names.get(end_str, None)
        if end is None:
            try:
                end = int(end_str)
            except ValueError:
                raise ValueError(f"Invalid range end: {end_str}")

        return set(range(start, end + 1)) & set(value_range)

    def _parse_step(self, step_str: str, value_range, field_index: int) -> set:
        """Parse step expressions like */5 or 10-50/5."""
        parts = step_str.split('/')
        if len(parts) != 2:
            raise ValueError(f"Invalid step expression: {step_str}")

        base_str, step_str = parts[0].strip(), parts[1].strip()
        values = list(value_range)

        try:
            step = int(step_str)
        except ValueError:
            raise ValueError(f"Invalid step value: {step_str}")

        if base_str == '*':
            return set(range(values[0], values[-1] + 1, step)) & set(values)

        # Handle ranged step like 10-50/5
        if '-' in base_str:
            base_range = self._parse_range(base_str, value_range, field_index)
            min_val = min(base_range)
            return set(range(min_val, max(base_range) + 1, step)) & base_range

        return set(range(int(base_str), values[-1] + 1, step)) & set(values)

    def _get_names_for_field(self, field_index: int) -> Dict[str, int]:
        """Get name mappings for month (3) and day of week (4) fields."""
        if field_index == 3:  # Month
            return self.MONTH_NAMES
        elif field_index == 4:  # Day of week
            return self.DAY_NAMES
        return {}

    def matches(self, dt: datetime = None) -> bool:
        """
        Check if a datetime matches this cron expression.

        Args:
            dt: Datetime to check (defaults to current time)

        Returns:
            True if the datetime matches the expression
        """
        if dt is None:
            dt = datetime.now()

        minute = dt.minute
        hour = dt.hour
        day = dt.day
        month = dt.month
        dow = dt.weekday()  # 0=Monday, 6=Sunday, convert to cron format (0=Sunday)
        dow = (dow + 1) % 7  # Convert to cron format

        # Check each field
        if minute not in self.fields[CronField.MINUTE]:
            return False
        if hour not in self.fields[CronField.HOUR]:
            return False
        if month not in self.fields[CronField.MONTH]:
            return False

        # Handle day and dow: if both specified (not ?), either can match
        day_specified = self.fields[CronField.DAY_OF_MONTH] != set(self.DAY_RANGE)
        dow_specified = self.fields[CronField.DAY_OF_WEEK] != set(self.DAY_OF_WEEK_RANGE)

        if day_specified and dow_specified:
            return (day in self.fields[CronField.DAY_OF_MONTH] or
                    dow in self.fields[CronField.DAY_OF_WEEK])
        elif day_specified:
            return day in self.fields[CronField.DAY_OF_MONTH]
        elif dow_specified:
            return dow in self.fields[CronField.DAY_OF_WEEK]

        return True

    def next_run(self, from_time: datetime = None) -> datetime:
        """
        Calculate the next run time for this expression.

        Args:
            from_time: Start time for calculation (defaults to now)

        Returns:
            Next datetime that matches this expression
        """
        if from_time is None:
            from_time = datetime.now()

        # Start from the next minute
        current = from_time.replace(second=0, microsecond=0) + timedelta(minutes=1)

        # Search for the next matching time (max 4 years to prevent infinite loops)
        for _ in range(365 * 24 * 60 * 4):
            if self.matches(current):
                return current
            current += timedelta(minutes=1)

        raise RuntimeError("Could not find next run time within 4 years")


class CronTask:
    """Represents a single cron-scheduled task."""

    def __init__(self, name: str, expression: str, command: str, enabled: bool = True):
        """
        Initialize a cron task.

        Args:
            name: Task identifier/name
            expression: Cron expression string
            command: Command to execute (format: "module:function_name" or "script:path")
            enabled: Whether this task is enabled
        """
        self.name = name
        self.expression = expression
        self.command = command
        self.enabled = enabled
        self.last_run: Optional[datetime] = None
        self.next_run: Optional[datetime] = None
        self._cron_expr = CronExpression(expression)
        self._update_next_run()

    @staticmethod
    def _parse_datetime(value: Any) -> Optional[datetime]:
        if not value:
            return None
        if isinstance(value, datetime):
            return value
        if isinstance(value, str):
            return datetime.fromisoformat(value)
        raise ValueError(f"Unsupported datetime value: {value!r}")

    def _update_next_run(self):
        """Calculate the next run time."""
        if self.last_run:
            self.next_run = self._cron_expr.next_run(self.last_run)
        else:
            self.next_run = self._cron_expr.next_run()

    def is_due(self) -> bool:
        """Check if this task is due to run now."""
        if not self.enabled:
            return False
        if self.next_run is None:
            return False
        return datetime.now() >= self.next_run

    def mark_run(self):
        """Mark this task as having run."""
        self.last_run = datetime.now()
        self._update_next_run()

    def to_dict(self) -> Dict[str, Any]:
        """Convert task to dictionary for storage."""
        return {
            'name': self.name,
            'expression': self.expression,
            'command': self.command,
            'enabled': self.enabled,
            'last_run': self.last_run.isoformat() if self.last_run else None,
            'next_run': self.next_run.isoformat() if self.next_run else None
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'CronTask':
        """Create a task from a dictionary."""
        task = CronTask(
            name=data['name'],
            expression=data['expression'],
            command=data['command'],
            enabled=data.get('enabled', True)
        )
        task.last_run = CronTask._parse_datetime(data.get('last_run'))
        next_run = CronTask._parse_datetime(data.get('next_run'))
        if next_run is not None:
            task.next_run = next_run
        else:
            task._update_next_run()
        return task


class CronScheduler:
    """Manages a collection of cron tasks."""

    def __init__(self):
        """Initialize the scheduler."""
        self.tasks: Dict[str, CronTask] = {}
        self._execution_callbacks: Dict[str, Callable[[], None]] = {}

    def add_task(self, task: CronTask):
        """Add a task to the scheduler."""
        self.tasks[task.name] = task

    def remove_task(self, name: str) -> bool:
        """Remove a task by name."""
        if name in self.tasks:
            del self.tasks[name]
            return True
        return False

    def get_task(self, name: str) -> Optional[CronTask]:
        """Get a task by name."""
        return self.tasks.get(name)

    def get_all_tasks(self) -> List[CronTask]:
        """Get all tasks."""
        return list(self.tasks.values())

    def get_due_tasks(self) -> List[CronTask]:
        """Get all tasks that are due to run."""
        return [task for task in self.tasks.values() if task.is_due()]

    def register_callback(self, command: str, callback: Callable[[], None]):
        """
        Register a callback for a specific command.

        Args:
            command: Command string that triggers this callback
            callback: Callable to execute
        """
        self._execution_callbacks[command] = callback

    def execute_task(self, task: CronTask) -> bool:
        """
        Execute a task.

        Args:
            task: Task to execute

        Returns:
            True if execution was successful or deferred
        """
        if task.command in self._execution_callbacks:
            try:
                self._execution_callbacks[task.command]()
                task.mark_run()
                return True
            except Exception as e:
                # Execution callback failed
                return False
        return False

    def load_from_dicts(self, task_dicts: List[Dict[str, Any]]):
        """Load tasks from a list of dictionaries."""
        for task_dict in task_dicts:
            try:
                task = CronTask.from_dict(task_dict)
                self.add_task(task)
            except Exception:
                # Skip invalid tasks
                pass

    def to_dicts(self) -> List[Dict[str, Any]]:
        """Convert all tasks to dictionaries for storage."""
        return [task.to_dict() for task in self.tasks.values()]

