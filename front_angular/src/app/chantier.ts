import { Ouvrier } from './ouvrier';

export class Chantier {
    id_chantier: number;
    name_chantier: string;
    start: string;
    end: string;
    adress: string;
    ouvriers: Ouvrier[];
  }