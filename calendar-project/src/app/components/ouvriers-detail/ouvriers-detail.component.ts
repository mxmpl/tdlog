import { Component, OnInit, Input } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Location } from '@angular/common';

import { Ouvrier }         from '../../ouvrier';
import { OuvrierService }  from '../../services/ouvrier.service';

@Component({
  selector: 'app-ouvriers-detail',
  templateUrl: './ouvriers-detail.component.html',
  styleUrls: [ './ouvriers-detail.component.css' ]
})
export class OuvrierDetailComponent implements OnInit {
  @Input() ouvrier: Ouvrier;

  constructor(
    private route: ActivatedRoute,
    private ouvrierService: OuvrierService,
    private location: Location
  ) {}

  ngOnInit(): void {
    this.getOuvrier();
  }

  getOuvrier(): void {
    const id = +this.route.snapshot.paramMap.get('id');
    this.ouvrierService.getOuvrier(id)
      .subscribe(ouvrier => this.ouvrier = ouvrier);
  }

  goBack(): void {
    this.location.back();
  }

 save(): void {
    this.ouvrierService.updateOuvrier(this.ouvrier)
      .subscribe(() => this.goBack());
  }
}
