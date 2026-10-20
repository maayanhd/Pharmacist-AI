import { test, before, after } from "node:test";
import assert from "node:assert/strict";
import type { Server } from "node:http";
import type { AddressInfo } from "node:net";
import { createApp } from "../src/app";

let server: Server;
let base: string;

before(async () => {
  server = createApp().listen(0);
  await new Promise((r) => server.once("listening", r));
  base = `http://127.0.0.1:${(server.address() as AddressInfo).port}`;
});

after(() => {
  server.close();
});

async function get(path: string) {
  const res = await fetch(base + path);
  return { status: res.status, body: (await res.json()) as any };
}

test("defaults: page 1, limit 20", async () => {
  const { status, body } = await get("/medications");
  assert.equal(status, 200);
  assert.equal(body.items.length, 20);
  assert.equal(body.total, 45);
  assert.equal(body.page, 1);
  assert.equal(body.limit, 20);
});

test("page and limit select the right slice", async () => {
  const { body } = await get("/medications?limit=10&page=2");
  assert.deepEqual(
    body.items.map((m: any) => m.id),
    Array.from({ length: 10 }, (_, i) => `m${i + 11}`),
  );
});

test("limit above 100 is clamped", async () => {
  const { status, body } = await get("/medications?limit=500");
  assert.equal(status, 200);
  assert.equal(body.limit, 100);
  assert.equal(body.items.length, 45);
});

test("q filters case-insensitively and total counts filtered results", async () => {
  const { body } = await get("/medications?q=AMOX");
  assert.equal(body.total, 5);
  assert.ok(body.items.every((m: any) => m.name.toLowerCase().includes("amox")));
});

test("q combines with pagination", async () => {
  const { body } = await get("/medications?q=amox&limit=2&page=3");
  assert.equal(body.total, 5);
  assert.equal(body.items.length, 1);
});

test("page past the end returns empty items", async () => {
  const { status, body } = await get("/medications?page=99");
  assert.equal(status, 200);
  assert.deepEqual(body.items, []);
  assert.equal(body.total, 45);
});

for (const bad of ["page=0", "page=-1", "page=abc", "limit=0", "limit=2.5", "limit=x"]) {
  test(`invalid ${bad} returns 400`, async () => {
    const { status, body } = await get(`/medications?${bad}`);
    assert.equal(status, 400);
    assert.equal(typeof body.error, "string");
  });
}
