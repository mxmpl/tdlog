import { Component, OnInit, Input } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Ouvrier }         from '../../ouvrier';
import { ChantierService } from '../../services/chantier.service';

@Component({
  selector: 'app-select-chantier',
  templateUrl: './select-chantier.component.html',
  styleUrls: ['./select-chantier.component.css']
})
export class SelectChantierComponent implements OnInit {
  @Input() chantiers_dispos: Map<string,any[]>;
  @Input() showMe: boolean;

  constructor(
  	private route: ActivatedRoute,
  	private chantierService: ChantierService
  	) { }

  ngOnInit() {
  	this.getChantiersDispos();
  }

  getChantiersDispos(): void {
  	const id = +this.route.snapshot.paramMap.get('id');
  	this.chantierService.getChantiersDispos(id)
  		.subscribe(chantiers_dispos => this.chantiers_dispos = chantiers_dispos)
  }

  getNames(): string[] {
  	return Array.from(Object.keys(this.chantiers_dispos));
  }
}