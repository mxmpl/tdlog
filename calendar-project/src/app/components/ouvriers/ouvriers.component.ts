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
    this.getHeroes();
  }

  getHeroes(): void {
    this.ouvrierService.getOuvriers()
    .subscribe(ouvriers => this.ouvriers = ouvriers);
  }

  add(name: string): void {
    name = name.trim();
    if (!name) { return; }
    this.ouvrierService.addOuvrier({ name } as Ouvrier)
      .subscribe(ouvrier => {
        this.ouvriers.push(ouvrier);
      });
  }

  delete(ouvrier: Ouvrier): void {
    this.ouvriers = this.ouvriers.filter(o => o !== ouvrier);
    this.ouvrierService.deleteOuvrier(ouvrier).subscribe();
  }

}