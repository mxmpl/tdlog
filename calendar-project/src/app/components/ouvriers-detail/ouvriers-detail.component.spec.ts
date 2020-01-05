import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { OuvrierDetailComponent } from './ouvriers-detail.component';

describe('OuvrierDetailComponent', () => {
  let component: OuvrierDetailComponent;
  let fixture: ComponentFixture<OuvrierDetailComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ OuvrierDetailComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(OuvrierDetailComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
