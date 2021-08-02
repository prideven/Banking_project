import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Router } from '@angular/router';
import { LoginService, UserParams } from 'src/app/core';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.scss']
})
export class RegisterComponent implements OnInit {
  public signupForm: FormGroup;
  constructor(private formBuilder: FormBuilder, private loginService: LoginService, private snackBar: MatSnackBar, private router: Router){
    this.signupForm = this.formBuilder.group({
      email: ['', Validators.email],
      password: ['', Validators.required],
      firstName: ['', Validators.required],
      lastName: ['', Validators.required],
      userName: ['', Validators.required],
      phoneNumber: ['', Validators.required],
      isAdmin: ['', Validators.required]
    });
   }
  
   register() {
    let formValue:UserParams;
    let password, username;
      formValue = this.signupForm.value;
      password = this.signupForm.controls.password.value;
    formValue['phoneNumber']= "+91" + formValue['phoneNumber'].toString();
    delete formValue['password'];

    this.loginService.registerUser(formValue, password, this.signupForm.controls.userName.value).subscribe(response => {
      if (response.success) {
        this.openSnackBar(response.data, 'mat-primary');
        this.router.navigate(['/login']);
      }
    },  error => {
      this.openSnackBar(error, 'mat-warn');
    });
  }

  openSnackBar(message: string, className: string) {
    this.snackBar.open(message, '', {
      duration: 5000,
      panelClass: ['mat-toolbar', className]
    });
  }
  ngOnInit(): void {
  }

}
