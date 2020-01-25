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

  nomChoisi: string;
  ouvrierChoisi: Ouvrier;
  show: boolean = false;

  heureDebMatin = "08";
  heureFinMatin = "12" ;
  heureDebAM = "14" ;
  heureFinAM = "18";

  heureFinChoisie = this.heureFinMatin ;

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
    this.show = true;
    this.nomChoisi = ouvrier.name_ouvrier;
    this.ouvrierChoisi = ouvrier;
  }

  //Pour rallonger un chantier
  add(name_chantier: string, start: string, startTime:string, end: string, endTime:string, adress: string): void {
    name_chantier = name_chantier.trim();
    if (start.substr(11,2) == this.heureFinAM) {
      //Si le chantier se terminait en fin d'apres-midi
      start = start.substr(8,2) + "/" + start.substr(5,2) + "/" + start.substr(0,4) + " " + this.heureDebAM + ":00:00";
    } else {
      // Si le chantier se terminait en fin de matinee
      start = (parseInt(start.substr(8,2))+1).toString() + "/" + start.substr(5,2) + "/" + start.substr(0,4) + " " + this.heureDebAM + ":00:00";
    }
    end = end + " " + endTime + ":00:00";
  
    if (!name_chantier) { return; }
    this.chantierService.addChantier({ name_chantier,start,end,adress } as Chantier)
      .subscribe(_ => this.getChantier());
  }

  deleteAttribution(chantier: Chantier) {
    if (confirm('Voulez-vous enlever '+this.ouvrierChoisi.name_ouvrier+' du chantier '+chantier.name_chantier+' ?')) {
    this.chantierService.deleteAttribution(this.ouvrierChoisi, chantier)
      .subscribe(_ => this.goBack());
    }
  } 
}
