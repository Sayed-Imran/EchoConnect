const domain = window.location.href.split('/')[2].split(':')[0];
const host_domain = window.location.host;

export class Config {
  public static get BASE_POINT_API(): string {
    return `http://${domain}`;
  }
  public static get BASE_POINT_AUTH(): string {
    return this.BASE_POINT_API + ":4500/authenticate"
  }
  public static API_ENDPOINTS: any = {
    "login": this.BASE_POINT_AUTH + "/login",
    "register": this.BASE_POINT_AUTH + "/register",
    "googleLogin": this.BASE_POINT_AUTH + "/google_login",
  }
}
