import { Injectable } from '@angular/core';
import { Subject } from 'rxjs/internal/Subject';

@Injectable({
  providedIn: 'root'
})
export class SharedService {
  public userLoggedIn = new Subject<boolean>();
  public showSpinner = new Subject<boolean>();
  public accountDetails = new Subject<boolean>();
  constructor() { }
}
