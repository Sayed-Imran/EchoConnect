import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PostboxComponent } from './postbox.component';

describe('PostboxComponent', () => {
  let component: PostboxComponent;
  let fixture: ComponentFixture<PostboxComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ PostboxComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(PostboxComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
