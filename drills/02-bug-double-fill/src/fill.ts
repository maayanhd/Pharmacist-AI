export interface Inventory {
  reserve(medicationId: string, qty: number): Promise<void>;
}

export interface FillResult {
  key: string;
  medicationId: string;
  qty: number;
}

export class FillService {
  private seen = new Map<string, FillResult>();

  constructor(private inventory: Inventory) {}

  async fill(key: string, medicationId: string, qty: number): Promise<FillResult> {
    const existing = this.seen.get(key);
    if (existing) return existing;

    await this.inventory.reserve(medicationId, qty);

    const result: FillResult = { key, medicationId, qty };
    this.seen.set(key, result);
    return result;
  }
}
