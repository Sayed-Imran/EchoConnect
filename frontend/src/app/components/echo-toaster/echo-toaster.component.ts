import { DefaultResponse } from './../../models/default-response';
import { Component } from '@angular/core';
import { EchoToasterService } from '../../services/echo-toaster.service';


@Component({
  selector: 'app-echo-toaster',
  templateUrl: './echo-toaster.component.html',
  styleUrls: ['./echo-toaster.component.scss']
})
export class EchoToasterComponent {

  constructor(public echoToasterService: EchoToasterService) { }

}
