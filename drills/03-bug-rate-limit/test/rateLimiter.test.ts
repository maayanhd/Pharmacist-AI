import { test } from "node:test";
import assert from "node:assert/strict";
import { RateLimiter } from "../src/rateLimiter";

function clock(start = 0) {
  let t = start;
  return { now: () => t, advance: (ms: number) => (t += ms) };
}

test("allows exactly `limit` calls per window", () => {
  const c = clock();
  const rl = new RateLimiter(3, 1000, c.now);
  assert.deepEqual([1, 2, 3, 4].map(() => rl.allow("u")), [true, true, true, false]);
});

test("keys are independent", () => {
  const c = clock();
  const rl = new RateLimiter(1, 1000, c.now);
  assert.equal(rl.allow("a"), true);
  assert.equal(rl.allow("b"), true);
  assert.equal(rl.allow("a"), false);
});

test("allowed again after the window passes", () => {
  const c = clock();
  const rl = new RateLimiter(2, 1000, c.now);
  rl.allow("u");
  rl.allow("u");
  assert.equal(rl.allow("u"), false);
  c.advance(1000);
  assert.equal(rl.allow("u"), true);
  assert.equal(rl.allow("u"), true);
  assert.equal(rl.allow("u"), false);
});

test("still blocked just before the window ends", () => {
  const c = clock();
  const rl = new RateLimiter(1, 1000, c.now);
  rl.allow("u");
  c.advance(999);
  assert.equal(rl.allow("u"), false);
});

test("hammering while blocked does not extend the block", () => {
  const c = clock();
  const rl = new RateLimiter(1, 1000, c.now);
  rl.allow("u");
  for (let i = 0; i < 50; i++) rl.allow("u");
  c.advance(1000);
  assert.equal(rl.allow("u"), true);
});
