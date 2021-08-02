import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AddAdminAccountComponent } from './add-admin-account.component';

describe('AddAdminAccountComponent', () => {
  let component: AddAdminAccountComponent;
  let fixture: ComponentFixture<AddAdminAccountComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ AddAdminAccountComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(AddAdminAccountComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
