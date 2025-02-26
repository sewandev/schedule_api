export interface Slot {
    start_time: string;
    end_time: string;
  }
  
  export interface MedicAvailability {
    medic_id: number;
    slots: Slot[];
  }
  
  export interface AvailabilityResponse {
    available_slots: MedicAvailability[];
  }