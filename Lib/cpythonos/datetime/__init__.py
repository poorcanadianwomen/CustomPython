"""datetime module for CustomPython OS.

Basic date and time types.
"""

import time as _time


# Constants
MINYEAR = 1
MAXYEAR = 9999
MAXDAYS = 3652425  # MAXYEAR * 365 + 23 leap days
MAXSECONDS = MAXDAYS * 24 * 3600

# Days in each month (non-leap year)
_DAYS_IN_MONTH = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
_DAYS_BEFORE_MONTH = [0]

dbm = 0
for _dim in _DAYS_IN_MONTH[1:]:
    _DAYS_BEFORE_MONTH.append(dbm)
    dbm += _dim
del dbm, _dim


def _is_leap(year):
    """Return True if year is a leap year."""
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


def _days_in_year(year):
    """Return the number of days in year."""
    return 366 if _is_leap(year) else 365


def _days_before_month(year, month):
    """Return the number of days before month in year."""
    assert 1 <= month <= 12
    return _DAYS_BEFORE_MONTH[month] + (month > 2 and _is_leap(year))


def _ymd2ord(year, month, day):
    """Convert year, month, day to proleptic Gregorian ordinal."""
    assert 1 <= month <= 12
    return (_days_before_month(year, month) + day)


def _ord2ymd(n):
    """Convert proleptic Gregorian ordinal to year, month, day."""
    400 * n + 399
    year = (n - 1) // 36524 * 400 + 1
    n -= _ymd2ord(year, 1, 1)
    if n < 0:
        year -= 1
        n = n + _days_in_year(year)
    else:
        days_in_year = _days_in_year(year)
        if n >= days_in_year:
            year += 1
            n -= days_in_year
    month = 1
    while month < 12:
        dim = _DAYS_IN_MONTH[month]
        if month == 2 and _is_leap(year):
            dim = 29
        if n < dim:
            break
        n -= dim
        month += 1
    day = n + 1
    return year, month, day


class timedelta:
    """Duration between two dates or times."""
    
    def __init__(self, days=0, seconds=0, microseconds=0, milliseconds=0,
                 minutes=0, hours=0, weeks=0):
        d = days + weeks * 7
        s = seconds + minutes * 60 + hours * 3600
        us = microseconds + milliseconds * 1000
        
        # Normalize
        total = d * 86400 + s
        seconds = total % 60
        total //= 60
        minutes = total % 60
        hours = total // 60
        
        # Handle microseconds
        microseconds += us
        microseconds += seconds * 1000000
        microseconds += minutes * 60000000
        microseconds += hours * 3600000000
        
        days = microseconds // (86400 * 1000000)
        microseconds %= 86400 * 1000000
        
        self._days = days
        self._seconds = microseconds // 1000000
        self._microseconds = microseconds % 1000000
    
    @property
    def days(self):
        return self._days
    
    @property
    def seconds(self):
        return self._seconds
    
    @property
    def microseconds(self):
        return self._microseconds
    
    def total_seconds(self):
        return self._days * 86400 + self._seconds + self._microseconds / 1000000
    
    def __repr__(self):
        if self._microseconds:
            return f'datetime.timedelta(days={self._days}, seconds={self._seconds}, microseconds={self._microseconds})'
        if self._seconds:
            return f'datetime.timedelta(days={self._days}, seconds={self._seconds})'
        return f'datetime.timedelta(days={self._days})'
    
    def __str__(self):
        mm, ss = divmod(self._seconds, 60)
        hh, mm = divmod(mm, 60)
        s = f'{self._days} day{"s" if self._days != 1 else ""}'
        if hh or mm or ss:
            s += f', {hh:02d}:{mm:02d}:{ss:02d}'
        if self._microseconds:
            s += f'.{self._microseconds:06d}'.rstrip('0')
        return s
    
    def __add__(self, other):
        if isinstance(other, timedelta):
            return timedelta(days=self._days + other._days,
                           seconds=self._seconds + other._seconds,
                           microseconds=self._microseconds + other._microseconds)
        return NotImplemented
    
    def __radd__(self, other):
        return self.__add__(other)
    
    def __sub__(self, other):
        if isinstance(other, timedelta):
            return timedelta(days=self._days - other._days,
                           seconds=self._seconds - other._seconds,
                           microseconds=self._microseconds - other._microseconds)
        return NotImplemented
    
    def __neg__(self):
        return timedelta(days=-self._days,
                        seconds=-self._seconds,
                        microseconds=-self._microseconds)
    
    def __pos__(self):
        return self
    
    def __abs__(self):
        if self._days < 0:
            return -self
        return self
    
    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return timedelta(days=self._days * other,
                           seconds=self._seconds * other,
                           microseconds=self._microseconds * other)
        return NotImplemented
    
    def __rmul__(self, other):
        return self.__mul__(other)
    
    def __floordiv__(self, other):
        if isinstance(other, timedelta):
            return (self._days * 86400 + self._seconds) // (other._days * 86400 + other._seconds)
        if isinstance(other, (int, float)):
            return timedelta(days=self._days // other,
                           seconds=self._seconds // other,
                           microseconds=self._microseconds // other)
        return NotImplemented
    
    def __truediv__(self, other):
        if isinstance(other, timedelta):
            return (self._days * 86400 + self._seconds + self._microseconds / 1000000) / \
                   (other._days * 86400 + other._seconds + other._microseconds / 1000000)
        if isinstance(other, (int, float)):
            return timedelta(days=self._days / other,
                           seconds=self._seconds / other,
                           microseconds=self._microseconds / other)
        return NotImplemented
    
    def __mod__(self, other):
        if isinstance(other, timedelta):
            r = self.total_seconds() % other.total_seconds()
            return timedelta(seconds=r)
        return NotImplemented
    
    def __eq__(self, other):
        if isinstance(other, timedelta):
            return (self._days == other._days and
                   self._seconds == other._seconds and
                   self._microseconds == other._microseconds)
        return NotImplemented
    
    def __ne__(self, other):
        return not self.__eq__(other)
    
    def __lt__(self, other):
        if isinstance(other, timedelta):
            return (self._days, self._seconds, self._microseconds) < \
                   (other._days, other._seconds, other._microseconds)
        return NotImplemented
    
    def __le__(self, other):
        if isinstance(other, timedelta):
            return (self._days, self._seconds, self._microseconds) <= \
                   (other._days, other._seconds, other._microseconds)
        return NotImplemented
    
    def __gt__(self, other):
        if isinstance(other, timedelta):
            return (self._days, self._seconds, self._microseconds) > \
                   (other._days, other._seconds, other._microseconds)
        return NotImplemented
    
    def __ge__(self, other):
        if isinstance(other, timedelta):
            return (self._days, self._seconds, self._microseconds) >= \
                   (other._days, other._seconds, other._microseconds)
        return NotImplemented
    
    def __bool__(self):
        return (self._days != 0 or self._seconds != 0 or self._microseconds != 0)
    
    def __hash__(self):
        return hash((self._days, self._seconds, self._microseconds))


# Pre-defined timedelta objects
timedelta.min = timedelta(days=-999999999)
timedelta.max = timedelta(days=999999999, hours=23, minutes=59, seconds=59, microseconds=999999)
timedelta.resolution = timedelta(microseconds=1)


class date:
    """Concrete date type."""
    
    def __init__(self, year, month, day):
        if not MINYEAR <= year <= MAXYEAR:
            raise ValueError(f'year is out of range: {year}')
        if not 1 <= month <= 12:
            raise ValueError(f'month is out of range: {month}')
        if not 1 <= day <= _DAYS_IN_MONTH[month]:
            if not (month == 2 and day == 29 and _is_leap(year)):
                raise ValueError(f'day is out of range: {day}')
        self._year = year
        self._month = month
        self._day = day
    
    @classmethod
    def fromtimestamp(cls, t):
        """Return the local date corresponding to the POSIX timestamp."""
        return cls.fromordinal(int(t) // 86400 + 719163)
    
    @classmethod
    def today(cls):
        """Return the current local date."""
        t = _time.time()
        return cls.fromtimestamp(t)
    
    @classmethod
    def fromordinal(cls, n):
        """Return the date corresponding to the proleptic Gregorian ordinal."""
        y, m, d = _ord2ymd(n)
        return cls(y, m, d)
    
    @classmethod
    def fromisoformat(cls, date_string):
        """Construct a date from a string in ISO 8601 format."""
        try:
            year = int(date_string[0:4])
            month = int(date_string[5:7])
            day = int(date_string[8:10])
            return cls(year, month, day)
        except (ValueError, IndexError):
            raise ValueError(f'Invalid isoformat string: {date_string!r}')
    
    @property
    def year(self):
        return self._year
    
    @property
    def month(self):
        return self._month
    
    @property
    def day(self):
        return self._day
    
    def replace(self, year=None, month=None, day=None):
        """Return a date with the same attributes, except those given new values."""
        if year is None:
            year = self._year
        if month is None:
            month = self._month
        if day is None:
            day = self._day
        return date(year, month, day)
    
    def timetuple(self):
        """Return a time.struct_time."""
        return time.struct_time(
            tm_year=self._year,
            tm_mon=self._month,
            tm_mday=self._day,
            tm_hour=0,
            tm_min=0,
            tm_sec=0,
            tm_wday=(self.toordinal() + 6) % 7,
            tm_yday=self._day_of_year(),
            tm_isdst=-1
        )
    
    def toordinal(self):
        """Return proleptic Gregorian ordinal."""
        return _ymd2ord(self._year, self._month, self._day)
    
    def weekday(self):
        """Return day of the week (0=Monday, 6=Sunday)."""
        return (self.toordinal() + 6) % 7
    
    def isoweekday(self):
        """Return day of the week (1=Monday, 7=Sunday)."""
        return self.weekday() + 1
    
    def isocalendar(self):
        """Return a 3-tuple (ISO year, ISO week number, ISO weekday)."""
        from math import floor
        ordinal = self.toordinal()
        year = self._year
        
        # Calculate ISO week number
        jan1 = date(year, 1, 1).toordinal()
        week_num = (ordinal - jan1) // 7 + 1
        weekday = self.isoweekday()
        
        # Adjust for year boundaries
        if week_num < 1:
            year -= 1
            week_num = date(year, 12, 28).isocalendar()[1]
        elif week_num > 52:
            if self._month == 12 and self._day >= 29:
                year += 1
                week_num = 1
        
        return (year, week_num, weekday)
    
    def isoformat(self):
        """Return ISO 8601 format string."""
        return f'{self._year:04d}-{self._month:02d}-{self._day:02d}'
    
    def __repr__(self):
        return f'datetime.date({self._year}, {self._month}, {self._day})'
    
    def __str__(self):
        return self.isoformat()
    
    def __format__(self, format_spec):
        if format_spec == '':
            return str(self)
        # TODO: implement strftime
        raise NotImplementedError('strftime not yet implemented')
    
    def __add__(self, other):
        if isinstance(other, timedelta):
            return self.fromordinal(self.toordinal() + other.days)
        return NotImplemented
    
    def __radd__(self, other):
        return self.__add__(other)
    
    def __sub__(self, other):
        if isinstance(other, timedelta):
            return self.fromordinal(self.toordinal() - other.days)
        if isinstance(other, date):
            return timedelta(days=self.toordinal() - other.toordinal())
        return NotImplemented
    
    def __eq__(self, other):
        if isinstance(other, date):
            return self._cmp(other) == 0
        return NotImplemented
    
    def __ne__(self, other):
        return not self.__eq__(other)
    
    def __lt__(self, other):
        if isinstance(other, date):
            return self._cmp(other) < 0
        return NotImplemented
    
    def __le__(self, other):
        if isinstance(other, date):
            return self._cmp(other) <= 0
        return NotImplemented
    
    def __gt__(self, other):
        if isinstance(other, date):
            return self._cmp(other) > 0
        return NotImplemented
    
    def __ge__(self, other):
        if isinstance(other, date):
            return self._cmp(other) >= 0
        return NotImplemented
    
    def _cmp(self, other):
        return (self._year, self._month, self._day).__cmp__((other._year, other._month, other._day))
    
    def __hash__(self):
        return hash((self._year, self._month, self._day))
    
    def _day_of_year(self):
        return _days_before_month(self._year, self._month) + self._day


# Pre-defined date objects
date.min = date(MINYEAR, 1, 1)
date.max = date(MAXYEAR, 12, 31)
date.resolution = timedelta(days=1)


class time:
    """Concrete time type."""
    
    def __init__(self, hour=0, minute=0, second=0, microsecond=0, tzinfo=None):
        if not 0 <= hour <= 23:
            raise ValueError(f'hour is out of range: {hour}')
        if not 0 <= minute <= 59:
            raise ValueError(f'minute is out of range: {minute}')
        if not 0 <= second <= 59:
            raise ValueError(f'second is out of range: {second}')
        if not 0 <= microsecond <= 999999:
            raise ValueError(f'microsecond is out of range: {microsecond}')
        
        self._hour = hour
        self._minute = minute
        self._second = second
        self._microsecond = microsecond
        self._tzinfo = tzinfo
    
    @property
    def hour(self):
        return self._hour
    
    @property
    def minute(self):
        return self._minute
    
    @property
    def second(self):
        return self._second
    
    @property
    def microsecond(self):
        return self._microsecond
    
    @property
    def tzinfo(self):
        return self._tzinfo
    
    def replace(self, hour=None, minute=None, second=None, microsecond=None):
        """Return a time with the same attributes."""
        if hour is None:
            hour = self._hour
        if minute is None:
            minute = self._minute
        if second is None:
            second = self._second
        if microsecond is None:
            microsecond = self._microsecond
        return time(hour, minute, second, microsecond)
    
    def isoformat(self):
        """Return ISO 8601 format string."""
        s = f'{self._hour:02d}:{self._minute:02d}:{self._second:02d}'
        if self._microsecond:
            s += f'.{self._microsecond:06d}'.rstrip('0')
        return s
    
    def __repr__(self):
        if self._microsecond:
            return f'datetime.time({self._hour}, {self._minute}, {self._second}, {self._microsecond})'
        if self._second:
            return f'datetime.time({self._hour}, {self._minute}, {self._second})'
        return f'datetime.time({self._hour}, {self._minute})'
    
    def __str__(self):
        return self.isoformat()
    
    def __eq__(self, other):
        if isinstance(other, time):
            return self._cmp(other) == 0
        return NotImplemented
    
    def __ne__(self, other):
        return not self.__eq__(other)
    
    def __lt__(self, other):
        if isinstance(other, time):
            return self._cmp(other) < 0
        return NotImplemented
    
    def __le__(self, other):
        if isinstance(other, time):
            return self._cmp(other) <= 0
        return NotImplemented
    
    def __gt__(self, other):
        if isinstance(other, time):
            return self._cmp(other) > 0
        return NotImplemented
    
    def __ge__(self, other):
        if isinstance(other, time):
            return self._cmp(other) >= 0
        return NotImplemented
    
    def _cmp(self, other):
        return (self._hour, self._minute, self._second, self._microsecond).__cmp__(
            (other._hour, other._minute, other._second, other._microsecond))
    
    def __hash__(self):
        return hash((self._hour, self._minute, self._second, self._microsecond))


# Pre-defined time objects
time.min = time(0, 0, 0)
time.max = time(23, 59, 59, 999999)
time.resolution = timedelta(microseconds=1)


class datetime(date):
    """Concrete date and time type."""
    
    def __init__(self, year, month, day, hour=0, minute=0, second=0,
                 microsecond=0, tzinfo=None):
        super().__init__(year, month, day)
        if not 0 <= hour <= 23:
            raise ValueError(f'hour is out of range: {hour}')
        if not 0 <= minute <= 59:
            raise ValueError(f'minute is out of range: {minute}')
        if not 0 <= second <= 59:
            raise ValueError(f'second is out of range: {second}')
        if not 0 <= microsecond <= 999999:
            raise ValueError(f'microsecond is out of range: {microsecond}')
        
        self._hour = hour
        self._minute = minute
        self._second = second
        self._microsecond = microsecond
        self._tzinfo = tzinfo
    
    @classmethod
    def now(cls, tz=None):
        """Return the current local date and time."""
        t = _time.time()
        return cls.fromtimestamp(t, tz)
    
    @classmethod
    def utcnow(cls):
        """Return the current UTC date and time."""
        t = _time.time()
        return cls.utcfromtimestamp(t)
    
    @classmethod
    def fromtimestamp(cls, t, tz=None):
        """Return the local date and time corresponding to the POSIX timestamp."""
        # Simple implementation
        return cls(1970, 1, 1) + timedelta(seconds=t)
    
    @classmethod
    def utcfromtimestamp(cls, t):
        """Return the UTC date and time corresponding to the POSIX timestamp."""
        return cls.fromtimestamp(t)
    
    @classmethod
    def combine(cls, date_obj, time_obj, tzinfo=None):
        """Combine date and time objects."""
        return cls(date_obj.year, date_obj.month, date_obj.day,
                  time_obj.hour, time_obj.minute, time_obj.second,
                  time_obj.microsecond, tzinfo)
    
    @classmethod
    def fromisoformat(cls, date_string):
        """Construct a datetime from a string in ISO 8601 format."""
        try:
            # Simple parsing
            date_part, time_part = date_string.split('T')
            year = int(date_part[0:4])
            month = int(date_part[5:7])
            day = int(date_part[8:10])
            
            if '+' in time_part or '-' in time_part:
                # Has timezone
                time_part = time_part[:8]  # Remove timezone for now
            
            if '.' in time_part:
                time_parts, microsecond = time_part.split('.')
                microsecond = int(microsecond.ljust(6, '0')[:6])
            else:
                time_parts = time_part
                microsecond = 0
            
            hour, minute, second = map(int, time_parts.split(':'))
            return cls(year, month, day, hour, minute, second, microsecond)
        except (ValueError, IndexError):
            raise ValueError(f'Invalid isoformat string: {date_string!r}')
    
    @property
    def hour(self):
        return self._hour
    
    @property
    def minute(self):
        return self._minute
    
    @property
    def second(self):
        return self._second
    
    @property
    def microsecond(self):
        return self._microsecond
    
    @property
    def tzinfo(self):
        return self._tzinfo
    
    def date(self):
        """Return date object with same year, month, day."""
        return date(self._year, self._month, self._day)
    
    def time(self):
        """Return time object with same hour, minute, second, microsecond."""
        return time(self._hour, self._minute, self._second, self._microsecond)
    
    def timetz(self):
        """Return time object with same hour, minute, second, microsecond and tzinfo."""
        return time(self._hour, self._minute, self._second, self._microsecond, self._tzinfo)
    
    def replace(self, year=None, month=None, day=None, hour=None, minute=None,
                second=None, microsecond=None, tzinfo=True):
        """Return a datetime with the same attributes."""
        if year is None:
            year = self._year
        if month is None:
            month = self._month
        if day is None:
            day = self._day
        if hour is None:
            hour = self._hour
        if minute is None:
            minute = self._minute
        if second is None:
            second = self._second
        if microsecond is None:
            microsecond = self._microsecond
        tzinfo = self._tzinfo if tzinfo is True else tzinfo
        return datetime(year, month, day, hour, minute, second, microsecond, tzinfo)
    
    def astimezone(self, tz=None):
        """Return a datetime with new tzinfo."""
        # Stub - needs proper timezone support
        return self
    
    def utcoffset(self):
        """Return UTC offset."""
        if self._tzinfo is None:
            return None
        return self._tzinfo.utcoffset(self)
    
    def tzname(self):
        """Return timezone name."""
        if self._tzinfo is None:
            return None
        return self._tzinfo.tzname(self)
    
    def dst(self):
        """Return DST offset."""
        if self._tzinfo is None:
            return None
        return self._tzinfo.dst(self)
    
    def isoformat(self, sep='T'):
        """Return ISO 8601 format string."""
        s = f'{self._year:04d}-{self._month:02d}-{self._day:02d}{sep}'
        s += f'{self._hour:02d}:{self._minute:02d}:{self._second:02d}'
        if self._microsecond:
            s += f'.{self._microsecond:06d}'.rstrip('0')
        if self._tzinfo is not None:
            offset = self._tzinfo.utcoffset(self)
            if offset is not None:
                s += str(offset)
        return s
    
    def __repr__(self):
        if self._microsecond:
            args = (self._year, self._month, self._day, self._hour,
                    self._minute, self._second, self._microsecond)
        elif self._second:
            args = (self._year, self._month, self._day, self._hour,
                    self._minute, self._second)
        else:
            args = (self._year, self._month, self._day, self._hour, self._minute)
        
        if self._tzinfo is not None:
            return f'datetime.datetime({", ".join(map(str, args))}, tzinfo={self._tzinfo!r})'
        return f'datetime.datetime({", ".join(map(str, args))})'
    
    def __str__(self):
        return self.isoformat()
    
    def __add__(self, other):
        if isinstance(other, timedelta):
            delta = timedelta(days=self.toordinal(),
                           seconds=self._hour * 3600 + self._minute * 60 + self._second,
                           microseconds=self._microsecond) + other
            return datetime.fromordinal(delta.days).replace(
                hour=(delta.seconds // 3600) % 24,
                minute=(delta.seconds // 60) % 60,
                second=delta.seconds % 60,
                microsecond=delta.microseconds)
        return NotImplemented
    
    def __radd__(self, other):
        return self.__add__(other)
    
    def __sub__(self, other):
        if isinstance(other, timedelta):
            return self.__add__(-other)
        if isinstance(other, datetime):
            days = self.toordinal() - other.toordinal()
            seconds = (self._hour * 3600 + self._minute * 60 + self._second) - \
                     (other._hour * 3600 + other._minute * 60 + other._second)
            microseconds = self._microsecond - other._microsecond
            return timedelta(days=days, seconds=seconds, microseconds=microseconds)
        return NotImplemented
    
    def __eq__(self, other):
        if isinstance(other, datetime):
            return date.__eq__(self, other) and \
                   (self._hour, self._minute, self._second, self._microsecond) == \
                   (other._hour, other._minute, other._second, other._microsecond)
        return NotImplemented
    
    def __ne__(self, other):
        return not self.__eq__(other)
    
    def __lt__(self, other):
        if isinstance(other, datetime):
            if date.__lt__(self, other):
                return True
            if date.__gt__(self, other):
                return False
            return (self._hour, self._minute, self._second, self._microsecond) < \
                   (other._hour, other._minute, other._second, other._microsecond)
        return NotImplemented
    
    def __le__(self, other):
        return self.__lt__(other) or self.__eq__(other)
    
    def __gt__(self, other):
        if isinstance(other, datetime):
            if date.__gt__(self, other):
                return True
            if date.__lt__(self, other):
                return False
            return (self._hour, self._minute, self._second, self._microsecond) > \
                   (other._hour, other._minute, other._second, other._microsecond)
        return NotImplemented
    
    def __ge__(self, other):
        return self.__gt__(other) or self.__eq__(other)
    
    def __hash__(self):
        return hash((self._year, self._month, self._day, self._hour,
                    self._minute, self._second, self._microsecond))


# Pre-defined datetime objects
datetime.min = datetime(MINYEAR, 1, 1)
datetime.max = datetime(MAXYEAR, 12, 31, 23, 59, 59, 999999)
datetime.resolution = timedelta(microseconds=1)


class timezone(timedelta):
    """Timezone class."""
    
    def __init__(self, offset, name=None):
        super().__init__(seconds=offset.total_seconds())
        self._name = name
    
    @classmethod
    def utc(cls):
        return cls(timedelta(0), 'UTC')
    
    @classmethod
    def utc(cls):
        return cls(timedelta(0), 'UTC')
    
    def utcoffset(self, dt):
        return self
    
    def tzname(self, dt):
        return self._name
    
    def dst(self, dt):
        return None
    
    def __repr__(self):
        return f'datetime.timezone({self._timedelta!r}, {self._name!r})'
    
    def __str__(self):
        return str(self._timedelta)


# Pre-defined timezone
timezone.utc = timezone.utc()
