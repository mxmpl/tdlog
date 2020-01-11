import { Component, OnInit, Input } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Location } from '@angular/common';

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
  showDates: boolean = false;

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
    this.ouvrierService.updateOuvrier(this.ouvrier)
      .subscribe(() => this.goBack());
  }

  toggleChantiersDispos(): void {
    this.ouvrierService.updateOuvrier(this.ouvrier);
    this.show = !this.show;
    this.showDates = false;
  }

  selectChantier(nom_chantier: string): void{
    this.showDates = true;
    this.nom_choisi = nom_chantier;
  }

  addAttribution(chantier: Chantier): void {
    this.chantierService.addAttribution(this.ouvrier, chantier)
      .subscribe(_ => this.ouvrierService.updateOuvrier(this.ouvrier));
  }
}
