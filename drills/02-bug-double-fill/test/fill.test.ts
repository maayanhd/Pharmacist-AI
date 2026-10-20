import { test } from "node:test";
import assert from "node:assert/strict";
import { FillService, type Inventory } from "../src/fill";

class FakeInventory implements Inventory {
  constructor(public stock: number) {}
  async reserve(_medicationId: string, qty: number): Promise<void> {
    await new Promise((r) => setImmediate(r));
    if (this.stock < qty) throw new Error("out of stock");
    this.stock -= qty;
  }
}

test("sequential duplicate key fills once", async () => {
  const inv = new FakeInventory(10);
  const svc = new FillService(inv);
  await svc.fill("k1", "med", 3);
  await svc.fill("k1", "med", 3);
  assert.equal(inv.stock, 7);
});

test("concurrent duplicate key fills once", async () => {
  const inv = new FakeInventory(10);
  const svc = new FillService(inv);
  const [a, b] = await Promise.all([svc.fill("k1", "med", 3), svc.fill("k1", "med", 3)]);
  assert.equal(inv.stock, 7);
  assert.deepEqual(a, b);
});

test("different keys each fill", async () => {
  const inv = new FakeInventory(10);
  const svc = new FillService(inv);
  await Promise.all([svc.fill("a", "med", 3), svc.fill("b", "med", 3)]);
  assert.equal(inv.stock, 4);
});

test("a failed fill does not poison the key", async () => {
  const inv = new FakeInventory(1);
  const svc = new FillService(inv);
  await assert.rejects(svc.fill("k1", "med", 3), /out of stock/);
  inv.stock = 10;
  const result = await svc.fill("k1", "med", 3);
  assert.equal(result.qty, 3);
  assert.equal(inv.stock, 7);
});

test("concurrent callers of a failing fill both see the failure", async () => {
  const inv = new FakeInventory(1);
  const svc = new FillService(inv);
  const results = await Promise.allSettled([svc.fill("k1", "med", 3), svc.fill("k1", "med", 3)]);
  assert.deepEqual(
    results.map((r) => r.status),
    ["rejected", "rejected"],
  );
});
