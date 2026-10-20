interface Entry {
  count: number;
  windowStart: number;
}

export class RateLimiter {
  private hits = new Map<string, Entry>();

  constructor(
    private limit: number,
    private windowMs: number,
    private now: () => number = Date.now,
  ) {}

  allow(key: string): boolean {
    const t = this.now();
    const entry = this.hits.get(key) ?? { count: 0, windowStart: t };

    if (t - entry.windowStart >= this.windowMs) {
      entry.windowStart = t;
    }

    entry.count++;
    this.hits.set(key, entry);
    return entry.count <= this.limit;
  }
}
