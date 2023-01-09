import { ComponentFixture, TestBed } from '@angular/core/testing';

import { EchoToasterComponent } from './echo-toaster.component';

describe('EchoToasterComponent', () => {
  let component: EchoToasterComponent;
  let fixture: ComponentFixture<EchoToasterComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ EchoToasterComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(EchoToasterComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
