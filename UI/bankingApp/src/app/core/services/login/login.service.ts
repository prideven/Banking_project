import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs/internal/Observable';
import { environment } from 'src/environments/environment';
import { URLConstants } from '../../rest-api-configuration';
import { AccountDetails, LoginResponse, RegisterResponse, UserParams } from './index';

@Injectable({
  providedIn: 'root'
})
export class LoginService {

  private baseUrl: string;
  constructor(private http: HttpClient) { 
    this.baseUrl = environment.url;
  }

  loginUser({username, password}): Observable<LoginResponse> {
    const httpHeaders: HttpHeaders = new HttpHeaders({
      Authorization: `Basic ${window.btoa(username + ':' + password)}`
  });
    return this.http.get<LoginResponse>(`${this.baseUrl}${URLConstants.LOGIN}`,{headers: httpHeaders});
  }


  registerUser(userDetails: UserParams, password:string, username:string):  Observable<RegisterResponse> {
    const httpHeaders: HttpHeaders = new HttpHeaders({
      Authorization: `Basic ${window.btoa(username + ':' + password)}`
  });
    return this.http.post<RegisterResponse>(`${this.baseUrl}${URLConstants.REGISTER}`, userDetails, {headers: httpHeaders}); 
    // return this.http.get<RegisterResponse>(`${this.baseUrl}${URLConstants.REGISTER}`,{headers: httpHeaders});
  }

  logout():Observable<any> {
    return this.http.get(`${this.baseUrl}${URLConstants.LOGOUT}`);
  }

 
  
}