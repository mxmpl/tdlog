import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ChantierDetailComponent } from './chantier-detail.component';

describe('ChantierDetailComponent', () => {
  let component: ChantierDetailComponent;
  let fixture: ComponentFixture<ChantierDetailComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ChantierDetailComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ChantierDetailComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
