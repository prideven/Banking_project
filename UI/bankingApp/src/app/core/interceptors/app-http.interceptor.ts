import { Injectable } from '@angular/core';
import {
  HttpRequest,
  HttpHandler,
  HttpEvent,
  HttpInterceptor,
  HttpResponse,
  HttpErrorResponse
} from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { SharedService } from '..';
import {catchError, map} from 'rxjs/operators'

@Injectable()
export class AppHttpInterceptor implements HttpInterceptor {

  constructor(private sharedService: SharedService) {}

  intercept(request: HttpRequest<unknown>, next: HttpHandler): Observable<HttpEvent<unknown>> {
    this.sharedService.showSpinner.next(true);
   // Get the auth token from the session.
   const authToken = sessionStorage.getItem('sessionID');


   // Clone the request and replace the original headers with
   // cloned headers, updated with the authorization.
   let newReq;
   if (authToken && !request.url.includes('login') && !request.url.includes('signup')) {
   const authReq = request.clone({
     headers: request.headers.set('Authorization',  `Bearer ${authToken}`)
   });
   newReq = authReq;
 } else {
   newReq = request;
 }

    // send cloned request with header to the next handler.
   return next.handle(newReq).pipe(catchError((error: HttpErrorResponse) => {
    let errorMessage = '';
    if (error.error instanceof ErrorEvent) {
      // client-side error
      errorMessage = `Error: ${error.error.message}`;
    } else {
      // server-side error
      if(error.error.data) {
      errorMessage = `Error Code: ${error.status}\nMessage: ${error.error.data}`;

      } else {
        errorMessage = `Error Code: ${error.status}\nMessage: ${error.message}`;

      }
    }
    this.sharedService.showSpinner.next(false);
    return throwError(errorMessage);
  }))
  .pipe(map<HttpEvent<any>, any>((evt: HttpEvent<any>) => {
    if (evt instanceof HttpResponse) {
      this.sharedService.showSpinner.next(false);
    return evt;

    }
  }));


  }
}
