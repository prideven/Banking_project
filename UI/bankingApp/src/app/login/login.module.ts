import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { LoginComponent } from './login/login.component';
import { RegisterComponent } from './register/register.component';
import { MaterialModule } from '../material/material.module';
import { RouterModule } from '@angular/router';
import { LoginRoutes } from './login.routes';



@NgModule({
  declarations: [LoginComponent, RegisterComponent],
  imports: [
    CommonModule,
    MaterialModule,
    RouterModule.forChild(LoginRoutes)
  ]
})
export class LoginModule { }
