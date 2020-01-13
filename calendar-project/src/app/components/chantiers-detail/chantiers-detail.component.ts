import { Component, OnInit, Input } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Location } from '@angular/common';

import { Chantier }        from '../../chantier';
import { ChantierService } from '../../services/chantier.service';
import { Ouvrier } from 'src/app/ouvrier';

@Component({
  selector: 'app-chantiers-detail',
  templateUrl: './chantiers-detail.component.html',
  styleUrls: ['./chantiers-detail.component.css']
})
export class ChantierDetailComponent implements OnInit {

  @Input() chantier: Chantier;

  nom_choisi: string;
  ouvrier_choisi: Ouvrier;
  horaires: Chantier[];
  show: boolean = false;

  constructor(
    private route: ActivatedRoute,
    private chantierService: ChantierService,
    private location: Location
  ) {}

  ngOnInit(): void {
    this.getChantier();
  }

  getChantier(): void {
    const id = this.route.snapshot.paramMap.get('name');
    this.chantierService.getChantier(id)
      .subscribe(chantier => this.chantier = chantier);
  }

  goBack(): void {
    this.location.back();
  }

  toggleHoraires(): void {
    this.show = !this.show;
  }

  selectOuvrier(ouvrier: Ouvrier): void{
    console.log('ok')
    this.show = true;
    this.nom_choisi = ouvrier.name_ouvrier;
    this.ouvrier_choisi = ouvrier;
    this.horaires = ouvrier.chantiers;
  }

  add(name_chantier: string, start: string, startTime:string, end: string, endTime:string, adress: string): void {
    name_chantier = name_chantier.trim();
    
    console.log(start.substr(11,2))
    if (start.substr(11,2) == "12") {
      console.log(start)
      start = start.substr(8,2) + "-" + start.substr(5,2) + "-" + start.substr(0,4) + " 14:00:00";
      console.log(start)

    } else {
      start = (parseInt(start.substr(8,2))+1).toString() + "-" + start.substr(5,2) + "-" + start.substr(0,4) + " 08:00:00";
      console.log(start)
    }
    end = end + " " + endTime + ":00:00";

  
    if (!name_chantier) { return; }
    this.chantierService.addChantier({ name_chantier,start,end,adress } as Chantier)
      .subscribe(_ => this.getChantier());
  }

  deleteAttribution(chantier: Chantier) {
    if (confirm('Voulez-vous enlever '+this.ouvrier_choisi.name_ouvrier+' du chantier '+chantier.name_chantier+' ?')) {
    this.chantierService.deleteAttribution(this.ouvrier_choisi, chantier)
      .subscribe(_ => this.goBack());
    }
  } 
}
