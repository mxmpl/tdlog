import { Component, OnInit } from '@angular/core';
import { Ouvrier }         from '../../ouvrier';
import { ChantierService } from '../../services/chantier.service';

@Component({
  selector: 'app-select-chantier',
  templateUrl: './select-chantier.component.html',
  styleUrls: ['./select-chantier.component.css']
})
export class SelectChantierComponent implements OnInit {
  chantiers_dispos: Map<string,any[]>;

  constructor(private ouvrier: Ouvrier, private chantierService: ChantierService) { }

  ngOnInit() {
  	this.getChantiersDispos();
  }

  getChantiersDispos(): void {
  	this.chantierService.getChantiersDispos(this.ouvrier.id_ouvrier)
  		.subscribe(chantiers_dispos => this.chantiers_dispos = chantiers_dispos)
  }
}
