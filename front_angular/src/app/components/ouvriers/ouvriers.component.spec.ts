import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { OuvriersComponent } from './ouvriers.component';

describe('OuvriersComponent', () => {
  let component: OuvriersComponent;
  let fixture: ComponentFixture<OuvriersComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ OuvriersComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(OuvriersComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
