import { Component, OnInit } from '@angular/core';
import { Chantier } from '../chantier';
import { ChantierService } from '../chantier.service';

@Component({
  selector: 'app-chantiers',
  templateUrl: './chantiers.component.html',
  styleUrls: ['./chantiers.component.css']
})

export class ChantiersComponent implements OnInit {

  selectedChantier: Chantier;
  chantiers: Chantier[];
  constructor(private chantierService: ChantierService) { }

  getChantiers(): void {
    this.chantierService.getChantiers()
        .subscribe(chantiers => this.chantiers = chantiers);
  }

  ngOnInit() {
  	this.getChantiers();
  }

  onSelect(chantier: Chantier): void {
  	this.selectedChantier = chantier;
  }
}
