import { TestBed } from '@angular/core/testing';

import { ChantierService } from './chantier.service';

describe('ChantierService', () => {
  beforeEach(() => TestBed.configureTestingModule({}));

  it('should be created', () => {
    const service: ChantierService = TestBed.get(ChantierService);
    expect(service).toBeTruthy();
  });
});
