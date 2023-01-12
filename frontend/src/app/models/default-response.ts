export class DefaultResponse {
  public status!: string;
  public message!: string;
  public data!: any;

  constructor(status: string = '', message: string = '', data: any = {}) {
    this.status = '';
    this.message = '';
    this.data = {};
  }
}
