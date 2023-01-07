import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { CommonUtils } from '../utils/common-utils';

@Injectable({ providedIn: 'root' })
export class HttpLayerService {

  constructor(private http: HttpClient) { }

  setDefaultHeaders(): HttpHeaders {
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Accept': 'application/json',
      'Authorization': 'Bearer ' + CommonUtils.getAuthToken(),
    });

    return headers;
  }

  public get(url: string): Observable<any> {
    return this.http.get(url, { headers: this.setDefaultHeaders() });
  }

  public post(url: string, data: any, options?: any): Observable<any> {
    return this.http.post(url, data, { headers: this.setDefaultHeaders(), ...options });
  }

  public put(url: string, data: any, options?: any): Observable<any> {
    return this.http.put(url, data, { headers: this.setDefaultHeaders(), ...options });
  }

  public delete(url: string): Observable<any> {
    return this.http.delete(url, { headers: this.setDefaultHeaders() });
  }

}
