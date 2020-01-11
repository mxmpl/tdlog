import { Component, OnInit } from '@angular/core';
import { Chantier } from 'src/app/chantier';
import { ChantierService } from 'src/app/services/chantier.service';

@Component({
  selector: 'app-chantiers',
  templateUrl: './chantiers.component.html',
  styleUrls: ['./chantiers.component.css']
})
export class ChantiersComponent implements OnInit {

  chantiers: Chantier[]

  constructor(private chantierService: ChantierService) { }

  ngOnInit() {
    this.getChantiers();
  }

  getChantiers(): void {
    this.chantierService.getChantiers()
    .subscribe(chantiers => this.chantiers = chantiers);
  }

  add(name_chantier: string): void {
    name_chantier = name_chantier.trim();
    if (!name_chantier) { return; }
    this.chantierService.addChantier({ name_chantier } as Chantier)
      .subscribe(_ => this.getChantiers());
  }

/*   delete(chantier: Chantier): void {
    this.chantiers = this.chantiers.filter(o => o !== chantier);
    this.chantierService.deleteChantier(chantier).subscribe();
  } */

}
