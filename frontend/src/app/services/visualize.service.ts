import { Observable } from 'rxjs';
import { Injectable } from '@angular/core';
import { HttpLayerService } from './http-layer.service';
import { Config } from '../config/config';

@Injectable({ providedIn: 'root' })
export class visualizeService {
  constructor(private httpLayerService: HttpLayerService) { }

  allPost(payload: any): Observable<any> {
    return this.httpLayerService.get(Config.API_ENDPOINTS['allCards']);
  }
}
