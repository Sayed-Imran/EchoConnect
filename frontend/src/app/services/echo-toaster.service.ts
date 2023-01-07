import { DefaultResponse } from '../models/default-response';
import { Injectable } from "@angular/core";


@Injectable({ providedIn: 'root' })
export class EchoToasterService {
  toasts: DefaultResponse[] = [];

  show(defaultResponse: DefaultResponse) {
    this.toasts.push(defaultResponse);
  }

  remove(toast: DefaultResponse) {
    this.toasts = this.toasts.filter(t => t != toast);
  }
}
