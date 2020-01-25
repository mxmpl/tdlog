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

  heureDebMatin = "08";
  heureFinMatin = "12" ;
  heureDebAM = "14" ;
  heureFinAM = "18";
  
  heureDebChoisie = this.heureDebMatin; //on initialise arbitraitement à 08
  heureFinChoisie = this.heureFinMatin;

  
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
    name_chantier = name_chantier[0].toUpperCase() + name_chantier.slice(1);
    start = start + " " + startTime + ":00:00";
    end = end + " " + endTime + ":00:00";
  
    if (!name_chantier) { return; }
    this.chantierService.addChantier({ name_chantier,start,end,adress } as Chantier)
      .subscribe(_ => this.getChantiers());
  }

   delete(chantier: Chantier): void {
    if (confirm('Voulez-vous supprimer le chantier '+chantier.name_chantier+' ?')) {
      this.chantiers = this.chantiers.filter(o => o !== chantier);
      this.chantierService.deleteChantier(chantier).subscribe();
    }
  } 

  

}
