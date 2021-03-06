import { Component, OnInit, Input } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Location } from '@angular/common';
import {MatListOption} from '@angular/material/list';

import { Ouvrier }         from '../../ouvrier';
import { Chantier }        from '../../chantier';
import { OuvrierService }  from '../../services/ouvrier.service';
import { ChantierService } from '../../services/chantier.service';

@Component({
  selector: 'app-ouvriers-detail',
  templateUrl: './ouvriers-detail.component.html',
  styleUrls: [ './ouvriers-detail.component.css' ]
})
export class OuvrierDetailComponent implements OnInit {
  @Input() ouvrier: Ouvrier;
  @Input() chantiers_dispos: Map<string,Chantier[]>;
  nom_choisi: string;
  show: boolean = false;
  chantiers_choisis: Chantier[] = [];

  constructor(
    private route: ActivatedRoute,
    private ouvrierService: OuvrierService,
    private chantierService: ChantierService,
    private location: Location
  ) {}

  ngOnInit(): void {
    this.getOuvrier();
    this.getChantiersDispos();
  }

  getOuvrier(): void {
    const id = +this.route.snapshot.paramMap.get('id');
    this.ouvrierService.getOuvrier(id)
      .subscribe(ouvrier => this.ouvrier = ouvrier);
  }

  getChantiersDispos(): void {
    const id = +this.route.snapshot.paramMap.get('id');
    this.chantierService.getChantiersDispos(id)
      .subscribe(chantiers_dispos => this.chantiers_dispos = chantiers_dispos)
  }

  getNames(): string[] {
    return Array.from(Object.keys(this.chantiers_dispos));
  }

  goBack(): void {
    this.location.back();
  }

  save(): void {
    if (confirm('Sauvegarder les changements ?')) {
      this.ouvrierService.updateOuvrier(this.ouvrier)
        .subscribe(() => this.goBack());
    }
  }

  toggleChantiersDispos(): void {
    this.ouvrierService.updateOuvrier(this.ouvrier);
    this.show = !this.show;
  }

  selectChantier(nom_chantier: string): void{
    this.show = true;
    this.nom_choisi = nom_chantier;
  }

  addAttributions(): void {
    if (confirm('Voulez-vous ajouter '+this.ouvrier.name_ouvrier+' à ces chantiers ?')) {
    this.chantierService.addAttributions(this.ouvrier, this.chantiers_choisis)
      .subscribe(_ => this.goBack());
    }
  }

   deleteAttribution(chantier: Chantier) {
    if (confirm('Voulez-vous enlever '+this.ouvrier.name_ouvrier+' du chantier '+chantier.name_chantier+' ?')) {
    this.chantierService.deleteAttribution(this.ouvrier, chantier)
      .subscribe(_ => this.goBack());
    }
  }
}
