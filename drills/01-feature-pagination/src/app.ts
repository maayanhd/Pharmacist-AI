import express from "express";

export interface Medication {
  id: string;
  name: string;
  dosageMg: number;
}

const names = [
  "Amoxicillin",
  "Ibuprofen",
  "Metformin",
  "Lisinopril",
  "Atorvastatin",
  "Omeprazole",
  "Amlodipine",
  "Sertraline",
  "Albuterol",
];

export const medications: Medication[] = Array.from({ length: 45 }, (_, i) => {
  const round = Math.floor(i / names.length);
  const base = names[i % names.length] as string;
  return {
    id: `m${i + 1}`,
    name: round === 0 ? base : `${base} ${round}`,
    dosageMg: 5 * (i + 1),
  };
});

export function createApp() {
  const app = express();

  app.get("/medications", (_req, res) => {
    res.json(medications);
  });

  return app;
}
