import { MatSnackBar } from '@angular/material/snack-bar';
import { LoginService, SharedService } from '../../core';
import { Component, OnInit, OnDestroy } from '@angular/core';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import { Subscription } from 'rxjs';
import { Router } from '@angular/router';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent implements OnInit, OnDestroy {
  public loginForm: FormGroup;
  private subscriptions = new Subscription();
  constructor(private formBuilder: FormBuilder, 
    private loginService: LoginService, 
    private router: Router, private snackBar: MatSnackBar, 
    private sharedService: SharedService
    ) {
   this.loginForm = this.formBuilder.group({
      username: ['', Validators.required],
      password: ['', Validators.required]
    });
   }
  ngOnInit() {
    const token = sessionStorage.getItem('sessionID');
    if(token && sessionStorage.getItem('accountDetails')) {
      this.sharedService.userLoggedIn.next(true);
      const usertype = JSON.parse(sessionStorage.getItem('accountDetails')).isAdmin;
      if(usertype) {
        this.router.navigate(['admin']);
      } else {
        this.router.navigate(['dashboard']);
      }
    }
  }

  openSnackBar(message: string, className: string) {
    this.snackBar.open(message, '', {
      duration: 5000,
      panelClass: ['mat-toolbar', className]
    });
  }

  
      


  onSubmit() {
    console.log('value', this.loginForm.value);
    this.subscriptions.add(this.loginService.loginUser(this.loginForm.value).subscribe(response => {
      if (response.success && response.data.accessToken) {
       sessionStorage.setItem('username', this.loginForm.value.username);
       sessionStorage.setItem('sessionID', response.data.accessToken);
       sessionStorage.setItem('accountDetails', JSON.stringify(response.data.profile))
       this.sharedService.userLoggedIn.next(true);
       if(response.data.profile.isAdmin) {
        this.router.navigate(['admin'])
      } else {
        this.router.navigate(['dashboard'])

      }
      }
    }, error => {
      this.openSnackBar(error, 'mat-warn');
    }));
  }

  ngOnDestroy() {
    this.subscriptions.unsubscribe();
  }

  goToRegister() {
    this.router.navigate(['login/register']);
  }
}
