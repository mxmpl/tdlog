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

  choixHeuresDeb = {"choix":[{"deb":"8h"},{"deb":"14h"}],"debut":"8h","fin":"12h"} //en cours

  constructor(private chantierService: ChantierService) { }

  ngOnInit() {
    this.getChantiers();
  }

  getChantiers(): void {
    this.chantierService.getChantiers()
    .subscribe(chantiers => this.chantiers = chantiers);
  }

  add(name_chantier: string, start: string, startTime:string, end: string, endTime:string, adress: string): void {
    name_chantier = name_chantier.trim();
    start = start + " " + startTime + ":00:00";
    end = end + " " + endTime + ":00:00";
  
    if (!name_chantier) { return; }
    this.chantierService.addChantier({ name_chantier,start,end,adress } as Chantier)
      .subscribe(_ => this.getChantiers());
  }

/*   delete(chantier: Chantier): void {
    this.chantiers = this.chantiers.filter(o => o !== chantier);
    this.chantierService.deleteChantier(chantier).subscribe();
  } */

}
