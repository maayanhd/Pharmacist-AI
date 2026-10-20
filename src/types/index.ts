export type UUID = string;

export type Role = "pharmacist" | "patient" | "admin";

export interface User {
  id: UUID;
  name: string;
  email: string;
  role: Role;
}

export interface Medication {
  id: UUID;
  name: string;
  dosageMg: number;
}

export interface Prescription {
  id: UUID;
  patientId: UUID;
  medicationId: UUID;
  status: "pending" | "filled" | "cancelled";
}
