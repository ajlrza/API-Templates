# API Template Scripts

> These were part of my previous projects that I didn't decide to continue, my intention is that they can be re-used for your projects.

* Waitlister API in TypeScript
* Key-Val DB API in Python with LMDB
* State Queue in Python with asyncio

# Custom LMDB Script

A lightweight Python key-value storage layer built on LMDB that provides fast, persistent reads and writes for structured application data. It serializes records to JSON, encodes integer and string keys into byte-ordered indexes, and automatically generates tagged indexes when none are supplied. It also supports batch retrieval of multiple records in a single cursor pass and offloads blocking operations to background threads so the main thread stays responsive.

Tech Stack

Language: ```Python```

Database: ```LMDB (Lightning Memory-Mapped Database```

Serialization: ```orjson, dataclasses (asdict)```

Features: ```Big-endian byte key encoding, auto-generated index tagging, cursor-based batch reads (getmulti), threaded I/O helper```

Use case: ```AI Applications, Read-Heavy Applications, ML Training```

# Waitlister API Script
A lightweight TypeScript backend built with the Hono web framework that manages product waitlist signups and incentivizes sharing through a built-in referral system. It assigns each subscriber a custom referral link, tracks successful referrals, and calculates real-time leaderboard queue rankings.

# Tech Stack
Language: ```TypeScript```

HTTP Framework: ```Hono```

Database & ORM: ```PostgreSQL, Drizzle ORM, postgres-js driver```

Features: ```Base62 encoding/decoding, SQL window functions, custom middleware rate limiting```

Use case: ```Start-up waitlisting page```

# State Queue Script

A lightweight Python state-management layer that buffers application state through an async queue and routes it into named, prioritized partitions. It separates state into main (observed), background (unobserved) and miscellaneous channels, persists each partition to a file-based partition pool, and tracks active partitions through a central manager. It also detects the host's CPU core count to set a processing level and includes a monitor that drains the buffer and reports any state left uncleared.

# Tech Stack

Language: Python

Concurrency: asyncio (bounded asyncio.Queue), multiprocessing

Storage: File-based partition pool

Features: Bounded hypervisor buffer (max 100), priority-tagged partitions (HIGH / MEDIUM / LOW) with UP / DOWN status, observed / unobserved / misc state channels, CPU core-level detection, buffer-drain monitor

Use case: Game & App State Syncing, Background Job Queues, Event / Telemetry Buffering
