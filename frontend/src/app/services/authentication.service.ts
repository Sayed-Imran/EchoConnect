import { Observable } from 'rxjs';
import { Injectable } from '@angular/core';
import { HttpLayerService } from './http-layer.service';
import { Config } from '../config/config';

@Injectable({ providedIn: 'root' })
export class AuthenticationService {
  constructor(private httpLayerService: HttpLayerService) { }

  login(payload: any): Observable<any> {
    return this.httpLayerService.post(Config.API_ENDPOINTS['login'], payload, {});
  }

  register(payload: any): Observable<any> {
    return this.httpLayerService.post(Config.API_ENDPOINTS['register'], payload, {});
  }

  googleLogin(payload: any): Observable<any> {
    return this.httpLayerService.post(Config.API_ENDPOINTS['googleLogin'], payload, {});
  }

}
