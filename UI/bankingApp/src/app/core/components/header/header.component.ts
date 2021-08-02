import { Component, OnInit } from '@angular/core';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Router } from '@angular/router';
import { AccountDetails, LoginService, SharedService } from '../../services';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.scss']
})
export class HeaderComponent implements OnInit {
public isLoggedIn:boolean = false;
userDetails: AccountDetails;
private sessionID: string;
  constructor(private loginservice: LoginService, private snackBar: MatSnackBar, private router: Router, private sharedService: SharedService) { }

  ngOnInit(): void {
    this.sessionID = sessionStorage.getItem('sessionID');
    if(this.sessionID ) {
      this.isLoggedIn = true;
    } else {
      this.isLoggedIn = false;
    }

    if(sessionStorage.getItem('accountDetails')) {
      this.userDetails = JSON.parse(sessionStorage.getItem('accountDetails'));
    }
    this.sharedService.userLoggedIn.subscribe(response => {
      this.isLoggedIn = response;
    })
  }
  openSnackBar(message: string, className: string) {
    this.snackBar.open(message, '', {
      duration: 5000,
      panelClass: ['mat-toolbar', className]
    });
  }


  logout() {
    this.loginservice.logout().subscribe(response => {
      if(response.success) {
        sessionStorage.clear();
        this.sharedService.userLoggedIn.next(false)
        this.router.navigate(['login']);
      }
    }, error => {
      this.openSnackBar(error.msg, 'mat-warn')
    })
  }


  goToHome() {
    if(this.isLoggedIn && sessionStorage.getItem('accountDetails')) {
      const isAdmin = JSON.parse(sessionStorage.getItem('accountDetails')).isAdmin;
      if(isAdmin) {
        this.router.navigate(['admin'])
      } else {
        this.router.navigate(['dashboard'])
      }
    }
  }


}
