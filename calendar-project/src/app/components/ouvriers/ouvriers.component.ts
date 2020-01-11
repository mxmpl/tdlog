import { Component, OnInit } from '@angular/core';

import { Ouvrier } from '../../ouvrier';
import { OuvrierService } from '../../services/ouvrier.service';

@Component({
  selector: 'app-ouvriers',
  templateUrl: './ouvriers.component.html',
  styleUrls: ['./ouvriers.component.css']
})

export class OuvriersComponent implements OnInit {
  ouvriers: Ouvrier[];

  constructor(private ouvrierService: OuvrierService) { }

  ngOnInit() {
    this.getOuvriers();
  }

  getOuvriers(): void {
    this.ouvrierService.getOuvriers()
    .subscribe(ouvriers => this.ouvriers = ouvriers);
  }

  add(name_ouvrier: string): void {
    name_ouvrier = name_ouvrier.trim();
    if (!name_ouvrier) { return; }
    this.ouvrierService.addOuvrier({ name_ouvrier } as Ouvrier)
      .subscribe(_ => this.getOuvriers());
  }

  delete(ouvrier: Ouvrier){
    if (confirm('Voulez-vous supprimer '+ouvrier.name_ouvrier+' ?')) {
    this.ouvriers = this.ouvriers.filter(o => o !== ouvrier);
    this.ouvrierService.deleteOuvrier(ouvrier).subscribe();
    }
  }
}