import { Component, OnInit, Input } from '@angular/core';
import { Ouvrier } from '../ouvriers/ouvriers.component';

@Component({
  selector: 'app-ouvriers-detail',
  templateUrl: './ouvriers-detail.component.html',
  styleUrls: ['./ouvriers-detail.component.css']
})

export class OuvrierDetailComponent implements OnInit {
  @Input() ouvrier: Ouvrier;

  constructor() { }

  ngOnInit() {
  }

}
