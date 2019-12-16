import { Injectable } from '@angular/core';
import { Observable, of } from 'rxjs';

import { Chantier } from './chantier';
import { CHANTIERS } from './faux-chantiers';
import { MessageService } from './message.service';

@Injectable({
  providedIn: 'root'
})

export class ChantierService {
  getChantiers(): Observable<Chantier[]> {
    this.messageService.add('ChantierService: chantiers récupérés');
    return of(CHANTIERS);
  }
  constructor(private messageService: MessageService) { }
}
