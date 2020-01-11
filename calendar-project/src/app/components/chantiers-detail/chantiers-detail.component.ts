import { Component, OnInit, Input } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Location } from '@angular/common';

import { Chantier }        from '../../chantier';
import { ChantierService } from '../../services/chantier.service';

@Component({
  selector: 'app-chantiers-detail',
  templateUrl: './chantiers-detail.component.html',
  styleUrls: ['./chantiers-detail.component.css']
})
export class ChantierDetailComponent implements OnInit {

  @Input() chantier: Chantier;
  nom_choisi: string;
  show: boolean = false;
  showDates: boolean = false;

  constructor(
    private route: ActivatedRoute,
    private chantierService: ChantierService,
    private location: Location
  ) {}

  ngOnInit(): void {
    this.getChantier();
  }

  getChantier(): void {
    const id = +this.route.snapshot.paramMap.get('id');
    this.chantierService.getChantier(id)
      .subscribe(chantier => this.chantier = chantier);
  }

  goBack(): void {
    this.location.back();
  }

/*   save(): void {
    this.chantierService.updateChantier(this.chantier)
      .subscribe(() => this.goBack());
  } */

}
