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
/* 
  getHorairesOuvrier(): void {
    const id = this.id_heure;
    this.chantierService.getChantiersDispos(id)
      .subscribe(chantiers_dispos => this.chantiers_dispos = chantiers_dispos)
  } */
/*   save(): void {
    this.chantierService.updateChantier(this.chantier)
      .subscribe(() => this.goBack());
  } */

}
