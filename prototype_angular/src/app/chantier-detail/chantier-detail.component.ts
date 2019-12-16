import { Chantier } from '../chantier';
import { Component, OnInit, Input } from '@angular/core';

@Component({
  selector: 'app-chantier-detail',
  templateUrl: './chantier-detail.component.html',
  styleUrls: ['./chantier-detail.component.css']
})
export class ChantierDetailComponent implements OnInit {
  @Input() chantier: Chantier;

  constructor() { }

  ngOnInit() {
  }

}
