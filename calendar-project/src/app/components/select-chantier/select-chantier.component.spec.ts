import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { SelectChantierComponent } from './select-chantier.component';

describe('SelectChantierComponent', () => {
  let component: SelectChantierComponent;
  let fixture: ComponentFixture<SelectChantierComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ SelectChantierComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(SelectChantierComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
